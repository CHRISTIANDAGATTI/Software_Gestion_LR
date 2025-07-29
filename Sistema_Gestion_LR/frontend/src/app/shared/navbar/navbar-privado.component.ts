import { Component } from '@angular/core';
import { AuthService } from '../../auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar-privado',
  templateUrl: './navbar-privado.component.html',
  styleUrls: ['./navbar-privado.component.scss']
})
export class NavbarPrivadoComponent {
  constructor(private authService: AuthService, private router: Router) {}

  async cerrarSesion() {
    await this.authService.signOut();
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['/home']).then(() => {
      window.location.reload();
    });
  }
}
