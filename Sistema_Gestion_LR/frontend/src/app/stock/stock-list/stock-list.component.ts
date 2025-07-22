import { Component, OnInit } from '@angular/core';
import { StockService } from '../stock.service';
import { Router } from '@angular/router';
// Eliminados imports de MatDialog y ConfirmDialogComponent

@Component({
  selector: 'app-stock-list',
  templateUrl: './stock-list.component.html'
})
export class StockListComponent implements OnInit {
  productos: any[] = [];

  // Variables para el modal flotante
  showConfirmModal: boolean = false;
  confirmModalData: { title: string; message: string; error?: string; id?: number } = { title: '', message: '' };

  constructor(
    private stockService: StockService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.cargarProductos();
  }

  cargarProductos() {
    this.stockService.getProducto().subscribe(data => {
      this.productos = data;
    });
  }

  eliminarProducto(id: number) {
    // Mostrar modal flotante de confirmación
    this.confirmModalData = {
      title: 'Eliminar producto',
      message: '¿Seguro que quieres eliminar este producto?',
      id
    };
    this.showConfirmModal = true;
  }

  confirmarEliminarProducto(confirm: boolean) {
    if (confirm && this.confirmModalData.id) {
      this.stockService.deleteProducto(this.confirmModalData.id).subscribe({
        next: () => {
          this.cargarProductos();
          this.showConfirmModal = false;
        },
        error: (err) => {
          let errorMsg = 'Error al eliminar el producto.';
          if (err?.error?.detail) {
            errorMsg = err.error.detail;
          }
          this.confirmModalData = {
            title: 'No se puede eliminar',
            message: 'No se pudo eliminar el producto.',
            error: errorMsg
          };
          // El modal sigue abierto mostrando el error
        }
      });
    } else {
      this.showConfirmModal = false;
    }
  }

}
