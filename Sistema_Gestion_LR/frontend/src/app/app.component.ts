import { Component, ChangeDetectorRef } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Frontend Angular';
  mostrarNavbarPublico = true;

  constructor(public router: Router, private cdr: ChangeDetectorRef) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.mostrarNavbarPublico =
          this.router.url === '/' ||
          this.router.url.startsWith('/home') ||
          this.router.url.startsWith('/login') ||
          this.router.url.startsWith('/registro');
        this.cdr.detectChanges();
      }
    });
  }
}