import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-registro',
  templateUrl: './registro.component.html',
  styleUrls: ['./registro.component.scss']
})
export class RegistroComponent {
  nombre: string = '';
  email: string = '';
  password: string = '';
  error: string = '';
  success: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  async onSubmit() {
    this.error = '';
    try {
      const { data, error } = await this.authService.signUp(this.email, this.password);
      if (error) {
        this.error = error.message;
      } else {
        // Si el registro en Supabase fue exitoso, registrar en el backend
        const user = data.user;
        const token = data.session?.access_token;
        if (user && token) {
          const usuarioPayload = {
            supabase_user_id: user.id,
            nombre: this.nombre,
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
          console.log('Respuesta registro backend:', result, response.status);
        }
        this.success = '¡Registro exitoso!';
        setTimeout(() => {
          this.router.navigate(['/home']);
        }, 1500);
      }
    } catch (e) {
      this.error = 'Error de conexión';
    }
  }

}
