import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-registro',
  templateUrl: './registro.component.html',
  styleUrls: ['./registro.component.scss']
})
export class RegistroComponent {
  username: string = '';
  full_name: string = '';
  email: string = '';
  password: string = '';
  dni: string = '';
  telefono: string = '';
  error: string = '';
  success: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  async onSubmit() {
    this.error = '';
    try {
      const { data, error } = await this.authService.signUpWithMetadata(
        this.email,
        this.password,
        this.username,
        this.full_name,
        this.dni,
        this.telefono
      );
      if (error) {
        this.error = error.message;
      } else if (!data?.user) {
        this.error = 'No se pudo registrar el usuario.';
      } else {
        this.success = '¡Registro exitoso!';
        setTimeout(() => {
          this.router.navigate(['/home']);
        }, 1500);
      }
    } catch (e: any) {
      this.error = e.message || 'Error de registro';
    }
  }
}
