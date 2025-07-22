import { Component, OnInit } from '@angular/core';
import { StockService } from '../stock.service';
import { Router } from '@angular/router';
// Eliminados imports de MatDialog y ConfirmDialogComponent

@Component({
  selector: 'app-categoria-list',
  templateUrl: './categoria-list.component.html',
  styleUrls: ['./categoria-list.component.css']
})
export class CategoriaListComponent implements OnInit {
  categorias: any[] = [];

  // Variables para el modal flotante
  showConfirmModal: boolean = false;
  confirmModalData: { title: string; message: string; error?: string; id?: number } = { title: '', message: '' };

  constructor(
    private stockService: StockService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.cargarCategorias();
  }

  cargarCategorias() {
    this.stockService.getCategoria().subscribe(data => {
      this.categorias = data;
    });
  }

  eliminarCategoria(id: number) {
    // Mostrar modal flotante de confirmación
    this.confirmModalData = {
      title: 'Eliminar categoría',
      message: '¿Seguro que quieres eliminar esta categoría?',
      id
    };
    this.showConfirmModal = true;
  }

  confirmarEliminarCategoria(confirm: boolean) {
    if (confirm && this.confirmModalData.id) {
      this.stockService.deleteCategoria(this.confirmModalData.id).subscribe({
        next: () => {
          this.cargarCategorias();
          this.showConfirmModal = false;
        },
        error: (err) => {
          let errorMsg = 'Error al eliminar la categoría.';
          if (err?.error?.detail) {
            errorMsg = err.error.detail;
          }
          this.confirmModalData = {
            title: 'No se puede eliminar',
            message: 'No se pudo eliminar la categoría.',
            error: errorMsg
          };
          // El modal sigue abierto mostrando el error
        }
      });
    } else {
      this.showConfirmModal = false;
    }
  }
  // Métodos duplicados eliminados

  editarCategoria(id: number) {
    this.router.navigate(['/stock/categoria/editar', id]);
  }
}
