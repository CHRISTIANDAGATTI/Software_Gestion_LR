import { Component } from '@angular/core';
import { AuthService } from '../../auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar-privado',
  templateUrl: './navbar-privado.component.html',
  styleUrls: ['./navbar-privado.component.scss']
})
export class NavbarPrivadoComponent {
  empresaNombre: string = '';
  username: string = '';
  isAdmin: boolean = false;

  constructor(private authService: AuthService, private router: Router) {
    this.cargarDatosUsuario();
  }

  async cargarDatosUsuario() {
    const user = await this.authService.getUser();
    if (user) {
      this.username = user.user_metadata?.username || user.email;
      this.empresaNombre = user.user_metadata?.empresa_nombre || '';
      this.isAdmin = user.user_metadata?.rol === 'admin';
    }
  }

  async cerrarSesion() {
    await this.authService.signOut();
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['/home']).then(() => {
      window.location.reload();
    });
  }
}
