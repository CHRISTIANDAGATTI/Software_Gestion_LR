import { Component, OnInit } from '@angular/core';
import { ProveedorService } from './proveedor.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-proveedor-list',
  templateUrl: './proveedor-list.component.html'
})
export class ProveedorListComponent implements OnInit {
  proveedores: any[] = [];
  busquedaNombre: string = '';
  busquedaDocumento: string = '';
  paginaActual: number = 1;
  proveedoresPorPagina: number = 25;

  constructor(private proveedorService: ProveedorService, private router: Router) {}

  ngOnInit(): void {
    this.cargarProveedores();
  }

  cargarProveedores() {
    this.proveedorService.getProveedores().subscribe(data => {
      this.proveedores = data;
    });
  }

  buscarProveedores() {
    let filtrados = this.proveedores;
    if (this.busquedaNombre) {
      filtrados = filtrados.filter(p => p.nombre?.toLowerCase().includes(this.busquedaNombre.toLowerCase()) || p.razon_social?.toLowerCase().includes(this.busquedaNombre.toLowerCase()));
    }
    if (this.busquedaDocumento) {
      filtrados = filtrados.filter(p => p.cuit?.includes(this.busquedaDocumento) || p.dni?.includes(this.busquedaDocumento));
    }
    return filtrados;
  }

  get totalPaginas(): number {
    return Math.ceil(this.buscarProveedores().length / this.proveedoresPorPagina) || 1;
  }

  proveedoresPaginados() {
    const inicio = (this.paginaActual - 1) * this.proveedoresPorPagina;
    return this.buscarProveedores().slice(inicio, inicio + this.proveedoresPorPagina);
  }

  cambiarPagina(nuevaPagina: number) {
    if (nuevaPagina >= 1 && nuevaPagina <= this.totalPaginas) {
      this.paginaActual = nuevaPagina;
    }
  }

  limpiarBusqueda() {
    this.busquedaNombre = '';
    this.busquedaDocumento = '';
    this.paginaActual = 1;
  }

  nuevoProveedor() {
    this.router.navigate(['proveedores/nuevo']);
  }

  editarProveedor(id: number) {
    this.router.navigate(['proveedores/editar', id]);
  }

  eliminarProveedor(id: number) {
    if (confirm('¿Seguro que desea eliminar este proveedor?')) {
      this.proveedorService.deleteProveedor(id).subscribe(() => {
        this.cargarProveedores();
      });
    }
  }
}
