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
    try {
      const { data, error } = await this.authService.signIn(this.email, this.password);
      console.log('Login Supabase:', data, error);
      if (error) {
        this.error = error.message;
      } else {
        // Intentar alta en la tabla usuarios si existe sesión y usuario
        const user = data.user;
        const token = data.session?.access_token;
        if (user && token) {
          const usuarioPayload = {
            supabase_user_id: user.id,
            nombre: user.user_metadata?.nombre || '',
            email: this.email
          };
          const response = await fetch('https://software-gestion-lr.onrender.com/api/v1/usuario/registrar', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(usuarioPayload)
          });
          const result = await response.json();
          console.log('Alta usuario backend:', result, response.status);
        }
        this.router.navigate(['/dashboard']);
      }
    } catch (e) {
      this.error = 'Error de conexión';
    }
  }

}
