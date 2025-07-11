import { Component } from '@angular/core';
import { StockService } from '../stock.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-categoria-form',
  templateUrl: './categoria-form.component.html'
})
export class CategoriaFormComponent {
  categoria: any = {};

  constructor(private stockService: StockService, private router: Router) {}

  guardar() {
    this.stockService.createCategoria(this.categoria).subscribe(() => {
      this.router.navigate(['/stock']);
    });
  }
}
