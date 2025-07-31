import { Injectable } from '@angular/core';
import { createClient, SupabaseClient, AuthError, AuthResponse, User } from '@supabase/supabase-js';
import { environment } from '../../environments/environment.prod';

@Injectable({ providedIn: 'root' })
export class AuthService {
  async getCurrentTenantId(): Promise<string | null> {
    const user = await this.getUser();
    if (!user) return null;
    // Prioridad: metadatos, luego perfil
    if (user.user_metadata?.tenant_id) {
      return user.user_metadata.tenant_id;
    }
    // Buscar en profiles si no está en metadatos
    const { data, error } = await this.supabase.from('profiles').select('tenant_id').eq('id', user.id).single();
    if (error || !data) return null;
    return data.tenant_id;
  }
  private supabase: SupabaseClient;

  constructor() {
    this.supabase = createClient(environment.supabaseUrl, environment.supabaseAnonKey);
  }

  async register(email: string, password: string, nombre: string) {
    const { data, error } = await this.supabase.auth.signUp({ email, password });
    if (error) {
      throw error;
    }
    if (data?.user) {
      const { error: insertError } = await this.supabase
        .from('usuarios')
        .insert([
          {
            id: data.user.id,
            email: data.user.email,
            nombre: nombre
          }
        ]);
      if (insertError) {
        console.warn('No se pudo insertar en usuarios:', insertError.message);
      }
    }
    return data;
  }

  async signIn(email: string, password: string): Promise<AuthResponse> {
    return await this.supabase.auth.signInWithPassword({ email, password });
  }

  async signOut(): Promise<{ error: AuthError | null }> {
    return await this.supabase.auth.signOut();
  }

  async getUser(): Promise<User | null> {
    const { data } = await this.supabase.auth.getUser();
    return data.user;
  }

  async getDemoTenantId(): Promise<string> {
    // Busca el tenant demo por nombre o CUIT fijo
    const { data, error } = await this.supabase.from('tenants').select('id').eq('nombre', 'Demo');
    if (error || !data || data.length === 0) {
      throw new Error('No se encontró el tenant demo');
    }
    return data[0].id;
  }

  async signUpWithMetadata(email: string, password: string, username: string, full_name: string, dni: string, telefono: string, empresa_nombre: string, empresa_cuit: string, tenant_id?: string) {
    // Si no se pasa tenant_id, busca el demo automáticamente
    let tenantId = tenant_id;
    if (!tenantId) {
      tenantId = await this.getDemoTenantId();
    }
    const { data, error } = await this.supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          username,
          full_name,
          dni,
          telefono,
          empresa_nombre,
          empresa_cuit,
          tenant_id: tenantId
        }
      }
    });
    // Si el registro fue exitoso, actualizar tenant_id en profiles
    if (data?.user?.id) {
      await this.supabase.from('profiles').update({ tenant_id: tenantId }).eq('id', data.user.id);
    }
    return { data, error };
  }

  async createEmpresaSolicitud(solicitud: { user_id: string, empresa_nombre: string, empresa_cuit: string }) {
    // Supabase: tabla solicitudes_acceso
    return await this.supabase.from('solicitudes_acceso').insert([
      {
        user_id: solicitud.user_id,
        empresa_nombre: solicitud.empresa_nombre,
        empresa_cuit: solicitud.empresa_cuit,
        estado: 'pendiente',
        fecha_solicitud: new Date().toISOString()
      }
    ]);
  }

  async isAdmin(): Promise<boolean> {
    const { data, error } = await this.supabase.auth.getUser();
    if (error || !data?.user) return false;
    return data.user.user_metadata?.rol === 'admin';
  }

  async aprobarSolicitudAcceso(solicitud: { user_id: string, empresa_cuit: string, empresa_nombre: string }) {
    // 1. Buscar el tenant por CUIT
    const { data: tenants } = await this.supabase.from('tenants').select('id').eq('cuit', solicitud.empresa_cuit);
    let tenantId;
    if (tenants && tenants.length > 0) {
      tenantId = tenants[0].id;
    } else {
      // Si no existe, crear el tenant
      const { data: nuevoTenant } = await this.supabase.from('tenants').insert({ nombre: solicitud.empresa_nombre, cuit: solicitud.empresa_cuit, habilitada: true, pago_validado: true }).select();
      tenantId = nuevoTenant[0].id;
    }
    // 2. Verificar si es el primer usuario de la empresa
    const { count } = await this.supabase.from('profiles').select('id', { count: 'exact' }).eq('tenant_id', tenantId);
    const isFirstUser = count === 0;
    // 3. Actualizar el perfil del usuario con el tenant_id
    await this.supabase.from('profiles').update({ tenant_id: tenantId }).eq('id', solicitud.user_id);
    // 4. Si es el primer usuario, asignar rol admin en los metadatos
    if (isFirstUser) {
      await this.supabase.auth.admin.updateUserById(solicitud.user_id, { user_metadata: { rol: 'admin' } });
    }
    // 5. Actualizar estado de la solicitud
    await this.supabase.from('solicitudes_acceso').update({ estado: 'aprobada' }).eq('user_id', solicitud.user_id);
  }
}
