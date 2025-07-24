import { Component, OnInit } from '@angular/core';
import { ClienteService } from '../cliente.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-cliente-form',
  templateUrl: './cliente-form.component.html'
})
export class ClienteFormComponent implements OnInit {
  cliente: any = {
    nombre: '',
    razon_social: '',
    cuit: '',
    dni: '',
    condicion_fiscal: '',
    telefono: '',
    email: '',
    direccion: '',
    localidad: '',
    provincia: '',
    observaciones: ''
  };
  editando: boolean = false;

  constructor(
    private clienteService: ClienteService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.editando = true;
      this.clienteService.getCliente(+id).subscribe({
        next: data => this.cliente = data,
        error: err => alert('Error al cargar cliente: ' + (err?.error?.detail || err.message))
      });
    }
  }

  guardarCliente() {
    if (this.editando) {
      // Aquí iría la lógica de edición
    } else {
      this.clienteService.createCliente(this.cliente).subscribe({
        next: () => this.router.navigate(['/clientes']),
        error: err => alert('Error al crear cliente: ' + (err?.error?.detail || err.message))
      });
    }
  }

  cancelar() {
    this.router.navigate(['/clientes']);
  }
}
