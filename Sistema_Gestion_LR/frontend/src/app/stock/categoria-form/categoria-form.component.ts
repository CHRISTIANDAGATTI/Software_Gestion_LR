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
    public route: ActivatedRoute,
    private router: Router,
    private stockService: StockService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.stockService.getCategoria().subscribe(data => {
        const cat = data.find((c: any) => c.id === id);
        if (cat) {
          this.categoria = { ...cat };
        }
      });
    } else {
      this.categoria = { nombre: '', descripcion: '' };
    }
  }

  guardarCambios() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.stockService.updateCategoria(id, this.categoria).subscribe(() => {
        alert('Categoría actualizada correctamente');
        this.router.navigate(['/stock']);
      });
    } else {
      this.stockService.createCategoria(this.categoria).subscribe(() => {
        alert('Categoría creada correctamente');
        this.router.navigate(['/stock']);
      });
    }
  }

  volver() {
    this.router.navigate(['/stock']);
  }
}
