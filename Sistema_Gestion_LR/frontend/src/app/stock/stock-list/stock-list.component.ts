import { Component, OnInit } from '@angular/core';
import { StockService } from '../stock.service';
import { Router } from '@angular/router';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
// Eliminados imports de MatDialog y ConfirmDialogComponent

@Component({
  selector: 'app-stock-list',
  templateUrl: './stock-list.component.html'
})
export class StockListComponent implements OnInit {
  productos: any[] = [];
  categorias: any[] = [];
  busquedaNombre: string = '';
  busquedaCodigo: string = '';
  busquedaCategoria: string = '';

  // Variables para el modal flotante
  showConfirmModal: boolean = false;
  confirmModalData: { title: string; message: string; error?: string; id?: number } = { title: '', message: '' };

  // Variables para paginación
  paginaActual: number = 1;
  productosPorPagina: number = 25;

  constructor(
    private stockService: StockService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.cargarProductos();
    this.cargarCategorias();
  }

  cargarProductos() {
    this.stockService.getProducto().subscribe(data => {
      this.productos = data;
    });
  }

  cargarCategorias() {
    this.stockService.getCategoria().subscribe(data => {
      this.categorias = data;
    });
  }

  buscarProductos() {
    let productosFiltrados = this.productos;
    if (this.busquedaNombre) {
      productosFiltrados = productosFiltrados.filter(p => p.nombre.toLowerCase().includes(this.busquedaNombre.toLowerCase()));
    }
    if (this.busquedaCodigo) {
      productosFiltrados = productosFiltrados.filter(p => p.codigo.toLowerCase().includes(this.busquedaCodigo.toLowerCase()));
    }
    if (this.busquedaCategoria) {
      productosFiltrados = productosFiltrados.filter(p => p.categoria && p.categoria.id == this.busquedaCategoria);
    }
    return productosFiltrados;
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

  exportarExcel() {
    const productos = this.buscarProductos().map(p => ({
      Código: p.codigo,
      Nombre: p.nombre,
      Descripción: p.descripcion,
      Categoría: p.categoria?.nombre,
      Cantidad: p.cantidad,
      Precio: p.precio
    }));
    const ws: XLSX.WorkSheet = XLSX.utils.json_to_sheet(productos);
    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Productos');
    const excelBuffer: any = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
    saveAs(blob, 'productos.xlsx');
  }

  get totalPaginas(): number {
    return Math.ceil(this.buscarProductos().length / this.productosPorPagina) || 1;
  }

  productosPaginados() {
    const inicio = (this.paginaActual - 1) * this.productosPorPagina;
    return this.buscarProductos().slice(inicio, inicio + this.productosPorPagina);
  }

  cambiarPagina(nuevaPagina: number) {
    if (nuevaPagina >= 1 && nuevaPagina <= this.totalPaginas) {
      this.paginaActual = nuevaPagina;
    }
  }

}
