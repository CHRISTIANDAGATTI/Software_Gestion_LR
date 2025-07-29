import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  email: string = '';
  password: string = '';
  error: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  async onSubmit() {
    this.error = '';
    this.error = '';
    try {
      const { data, error } = await this.authService.signIn(this.email, this.password);
      console.log('Login Supabase:', data, error);
      if (error) {
        this.error = error.message;
      } else {
        // ...eliminada lógica de alta en usuarios...
        // Recargar usuario y navegar al dashboard
        await this.authService.getUser();
        this.router.navigate(['/dashboard']);
      }
    } catch (e) {
      this.error = 'Error de conexión con Supabase';
    }
  }
}
