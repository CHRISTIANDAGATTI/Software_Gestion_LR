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
  empresa_nombre: string = '';
  empresa_cuit: string = '';
  error: string = '';
  success: string = '';

  constructor(private authService: AuthService, private router: Router) {}


  async onSubmit() {
    this.error = '';
    this.success = '';
    // Validaciones previas
    if (!this.username || !this.full_name || !this.dni || !this.telefono || !this.email || !this.password || !this.empresa_nombre || !this.empresa_cuit) {
      this.error = 'Todos los campos son obligatorios.';
      return;
    }
    if (!/^[a-zA-Z0-9_]+$/.test(this.username)) {
      this.error = 'El nombre de usuario no debe tener espacios ni caracteres especiales.';
      return;
    }
    if (this.username.length < 4) {
      this.error = 'El nombre de usuario debe tener al menos 4 caracteres.';
      return;
    }
    if (this.full_name.trim().split(/\s+/).length < 2) {
      this.error = 'El nombre completo debe tener al menos dos palabras.';
      return;
    }
    if (!/^\d{7,}$/.test(this.dni)) {
      this.error = 'El DNI debe ser numérico y tener al menos 7 dígitos.';
      return;
    }
    if (!/^\d{6,}$/.test(this.telefono)) {
      this.error = 'El teléfono debe ser numérico y tener al menos 6 dígitos.';
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
    // Limpiar CUIT (quitar guiones y espacios)
    const cuitLimpio = this.empresa_cuit.replace(/[-\s]/g, '');
    if (!/^\d{11}$/.test(cuitLimpio)) {
      this.error = 'El CUIT debe ser numérico y tener 11 dígitos.';
      return;
    }
    try {
      // Registrar usuario en tenant demo (id demo se obtiene automáticamente)
      const { data, error } = await this.authService.signUpWithMetadata(
        this.email,
        this.password,
        this.username,
        this.full_name,
        this.dni,
        this.telefono,
        this.empresa_nombre,
        cuitLimpio
      );
      if (error) {
        this.error = error.message;
      } else if (!data?.user) {
        this.error = 'No se pudo registrar el usuario.';
      } else {
        // Crear solicitud de relación con empresa
        await this.authService.createEmpresaSolicitud({
          user_id: data.user.id,
          empresa_nombre: this.empresa_nombre,
          empresa_cuit: cuitLimpio
        });
        this.success = '¡Registro exitoso! Ahora puedes probar el sistema en modo demo. Tu solicitud de acceso a la empresa será revisada.';
        setTimeout(() => {
          this.router.navigate(['/home']);
        }, 2000);
      }
    } catch (e: any) {
      this.error = e.message || 'Error de registro';
    }
  }
}
