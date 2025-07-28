import { Component, ChangeDetectorRef } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { AuthService } from './auth/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Frontend Angular';
  mostrarNavbarPublico = true;

  constructor(public router: Router, private cdr: ChangeDetectorRef, private authService: AuthService) {
    this.router.events.subscribe(async event => {
      if (event instanceof NavigationEnd) {
        const user = await this.authService.getUser();
        this.mostrarNavbarPublico = !user;
        this.cdr.detectChanges();
      }
    });
  }
}