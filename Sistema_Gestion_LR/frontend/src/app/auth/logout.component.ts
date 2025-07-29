import { Component } from '@angular/core';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-logout',
  template: `<button (click)="cerrarSesion()">Cerrar sesión</button>`
})
export class LogoutComponent {
  constructor(private authService: AuthService, private router: Router) {}

  async cerrarSesion() {
    await this.authService.signOut();
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['/login']);
    window.location.reload();
  }
}
