import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StockService } from '../stock.service';

@Component({
  selector: 'app-categoria-form',
  templateUrl: './categoria-form.component.html'
})
export class CategoriaFormComponent implements OnInit {
  producto: any = null;
  categorias: any[] = [];
  categoriaActualNombre: string = '';
  nuevaCategoriaId: number|null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private stockService: StockService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    // Cargar todas las categorías para el select
    this.stockService.getCategoria().subscribe(data => {
      this.categorias = data;
      // Cargar el producto actual
      this.stockService.getProducto(id).subscribe(prod => {
        this.producto = prod;
        this.categoriaActualNombre = prod.categoria?.nombre || '';
        this.nuevaCategoriaId = prod.categoria?.id || null;
      });
    });
  }

  guardarCambios() {
    if (!this.producto) return;
    const id = Number(this.route.snapshot.paramMap.get('id'));
    const productoActualizado = { categoria_id: this.nuevaCategoriaId };
    this.stockService.updateProducto(id, { ...this.producto, ...productoActualizado }).subscribe(() => {
      this.router.navigate(['/stock']);
    });
  }
}
