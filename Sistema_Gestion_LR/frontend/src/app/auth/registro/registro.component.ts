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
      const data = await this.authService.register(this.email, this.password, this.nombre);
      if (!data?.user) {
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
