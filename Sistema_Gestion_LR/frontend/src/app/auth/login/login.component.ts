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

  constructor(private authService: AuthService, private router: Router) {}

  async onSubmit() {
    this.error = '';
    try {
      const { error } = await this.authService.signIn(this.email, this.password);
      if (error) {
        this.error = error.message;
      } else {
        this.router.navigate(['/dashboard']);
      }
    } catch (e) {
      this.error = 'Error de conexión';
    }
  }

}
