import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/auth/auth.service';

@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.scss']
})
export class AdminPanelComponent implements OnInit {
  isAdmin: boolean = false;

  constructor(private authService: AuthService) {}

  async ngOnInit() {
    this.isAdmin = await this.authService.isAdmin();
  }
}
