import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StockService } from '../stock.service';

@Component({
  selector: 'app-producto-form',
  templateUrl: './producto-form.component.html'
})
export class ProductoFormComponent implements OnInit {
  producto: any = { nombre: '', descripcion: '', precio: 0, categoria_id: null };
  categorias: any[] = [];
  isEdit: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private stockService: StockService
  ) {}

  ngOnInit(): void {
    // Cargar categorías
    this.stockService.getCategoria().subscribe(cats => {
      this.categorias = cats;
      // Si es edición, cargar producto
      const id = this.route.snapshot.paramMap.get('id');
      if (id) {
        this.isEdit = true;
        this.stockService.getProducto(Number(id)).subscribe(data => {
          this.producto = data;
          // Si la categoría viene anidada, tomar solo el id
          if (this.producto.categoria && typeof this.producto.categoria === 'object') {
            this.producto.categoria_id = this.producto.categoria.id;
          }
        });
      }
    });
  }

  guardar() {
    if (this.isEdit) {
      this.stockService.updateProducto(this.producto.id, this.producto).subscribe(() => {
        this.router.navigate(['/stock']);
      });
    }
  }
}
