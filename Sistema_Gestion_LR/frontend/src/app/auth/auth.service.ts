import { Injectable } from '@angular/core';
import { createClient, SupabaseClient, AuthError, AuthResponse, User } from '@supabase/supabase-js';
import { environment } from '../../environments/environment.prod';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private supabase: SupabaseClient;

  constructor() {
    this.supabase = createClient(environment.supabaseUrl, environment.supabaseAnonKey);
  }

  async signUp(email: string, password: string): Promise<AuthResponse> {
    return await this.supabase.auth.signUp({ email, password });
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
