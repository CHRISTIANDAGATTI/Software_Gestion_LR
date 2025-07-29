import { Injectable } from '@angular/core';
import { createClient, SupabaseClient, AuthError, AuthResponse, User } from '@supabase/supabase-js';
import { environment } from '../../environments/environment.prod';

@Injectable({ providedIn: 'root' })
export class AuthService {
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
}
