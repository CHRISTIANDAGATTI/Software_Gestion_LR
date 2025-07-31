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
  success: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  async onSubmit() {
    this.error = '';
    this.success = '';
    // Validaciones previas
    if (!this.email || !this.password) {
      this.error = 'Email y contraseña son obligatorios.';
      return;
    }
    if (!/^\S+@\S+\.\S+$/.test(this.email)) {
      this.error = 'El formato del email es inválido.';
      return;
    }
    if (this.password.length < 6) {
      this.error = 'La contraseña debe tener al menos 6 caracteres.';
      return;
    }
    try {
      const { data, error } = await this.authService.signIn(this.email, this.password);
      if (error) {
        if (error.message?.toLowerCase().includes('invalid login credentials') || error.message?.toLowerCase().includes('invalid email or password')) {
          this.error = 'Email o contraseña incorrectos.';
        } else if (error.message?.toLowerCase().includes('email')) {
          this.error = 'El email ingresado no es válido.';
        } else {
          this.error = error.message;
        }
      } else if (!data?.user) {
        this.error = 'No se pudo iniciar sesión.';
      } else {
        this.success = '¡Ingreso exitoso!';
        setTimeout(() => {
          this.router.navigate(['/home']);
        }, 1200);
      }
    } catch (e: any) {
      this.error = e.message || 'Error al iniciar sesión';
    }
  }
}
