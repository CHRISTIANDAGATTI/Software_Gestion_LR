import { Component, OnInit } from '@angular/core';
import { StockService } from '../stock.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-stock-list',
  templateUrl: './stock-list.component.html'
})
export class StockListComponent implements OnInit {
  productos: any[] = [];

  constructor(private stockService: StockService, private router: Router) { }

  ngOnInit(): void {
    this.cargarProductos();
  }

  cargarProductos() {
    this.stockService.getProducto().subscribe(data => {
      this.productos = data;
    });
  }

  eliminarProducto(id: number) {
    if (confirm('¿Seguro que quieres eliminar este producto?')) {
      this.stockService.deleteProducto(id).subscribe(() => {
        this.cargarProductos(); // recargar lista
      });
    }
  }

  editarCategoria(idCategoria: number) {
    // Navegar al formulario de edición de categoría
    this.router.navigate(['/stock/categoria/editar', idCategoria]);
  }

  eliminarCategoria(id: number) {
    if (confirm('¿Seguro que quieres eliminar esta categoria?')) {
      this.stockService.deleteCategoria(id).subscribe(() => {
        this.cargarProductos(); // recargar lista
      });
    }
  }

}
