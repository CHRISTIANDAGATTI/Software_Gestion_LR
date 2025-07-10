import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StockService } from '../stock.service';

@Component({
  selector: 'app-categoria-form',
  templateUrl: './categoria-form.component.html'
})
export class CategoriaFormComponent implements OnInit {
  categoria: any = {
    nombre: ''
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private stockService: StockService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.stockService.getCategoria().subscribe(data => {
      this.categoria = data;
    });
  }

  guardarCambios() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.stockService.updateCategoria(id, this.categoria).subscribe(() => {
      alert('Categoría actualizada correctamente');
      this.router.navigate(['/stock']); // volver al listado
    });
  }
}
