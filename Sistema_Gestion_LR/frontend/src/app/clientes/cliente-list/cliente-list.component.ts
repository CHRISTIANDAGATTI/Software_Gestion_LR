import { Component, OnInit } from '@angular/core';
import { ClienteService } from '../cliente.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-cliente-list',
  templateUrl: './cliente-list.component.html'
})
export class ClienteListComponent implements OnInit {
  clientes: any[] = [];
  busquedaNombre: string = '';
  busquedaDocumento: string = '';
  paginaActual: number = 1;
  clientesPorPagina: number = 25;

  constructor(
    private clienteService: ClienteService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.cargarClientes();
  }

  cargarClientes() {
    this.clienteService.getClientes().subscribe(data => {
      this.clientes = data;
    });
  }

  buscarClientes() {
    let filtrados = this.clientes;
    if (this.busquedaNombre) {
      filtrados = filtrados.filter(c => c.nombre?.toLowerCase().includes(this.busquedaNombre.toLowerCase()) || c.razon_social?.toLowerCase().includes(this.busquedaNombre.toLowerCase()));
    }
    if (this.busquedaDocumento) {
      filtrados = filtrados.filter(c => c.cuit?.includes(this.busquedaDocumento) || c.dni?.includes(this.busquedaDocumento));
    }
    return filtrados;
  }

  get totalPaginas(): number {
    return Math.ceil(this.buscarClientes().length / this.clientesPorPagina) || 1;
  }

  clientesPaginados() {
    const inicio = (this.paginaActual - 1) * this.clientesPorPagina;
    return this.buscarClientes().slice(inicio, inicio + this.clientesPorPagina);
  }

  cambiarPagina(nuevaPagina: number) {
    if (nuevaPagina >= 1 && nuevaPagina <= this.totalPaginas) {
      this.paginaActual = nuevaPagina;
    }
  }

  eliminarCliente(id: number) {
    // Aquí puedes agregar lógica de confirmación si lo deseas
    this.clienteService.deleteCliente(id).subscribe(() => {
      this.cargarClientes();
    });
  }
}
