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
    // Validaciones previas
    if (!this.cliente.nombre && !this.cliente.razon_social) {
      alert('Debe completar al menos Nombre o Razón social.');
      return;
    }
    if (this.cliente.condicion_fiscal && this.cliente.condicion_fiscal !== 'Consumidor Final' && !this.cliente.cuit) {
      alert('Si la condición fiscal no es Consumidor Final, debe ingresar el CUIT.');
      return;
    }
    if (!this.cliente.cuit && !this.cliente.dni) {
      alert('Debe completar al menos CUIT o DNI.');
      return;
    }
    if (this.cliente.dni && !/^\d{7,}$/.test(this.cliente.dni)) {
      alert('El DNI debe ser numérico y tener al menos 7 dígitos.');
      return;
    }
    if (this.cliente.cuit && !/^\d{11}$/.test(this.cliente.cuit)) {
      alert('El CUIT debe ser numérico y tener 11 dígitos.');
      return;
    }
    if (this.cliente.telefono && !/^\d{6,}$/.test(this.cliente.telefono)) {
      alert('El teléfono debe ser numérico y tener al menos 6 dígitos.');
      return;
    }
    if (this.cliente.email && !/^\S+@\S+\.\S+$/.test(this.cliente.email)) {
      alert('El formato del email es inválido.');
      return;
    }
    if (this.editando) {
      // Aquí iría la lógica de edición
    } else {
      this.clienteService.createCliente(this.cliente).subscribe({
        next: () => this.router.navigate(['/clientes']),
        error: err => {
          if (err?.error?.detail?.toLowerCase().includes('duplicate') || err?.error?.detail?.toLowerCase().includes('ya existe')) {
            alert('El email o CUIT ya está registrado.');
          } else {
            alert('Error al crear cliente: ' + (err?.error?.detail || err.message));
          }
        }
      });
    }
  }

  cancelar() {
    this.router.navigate(['/clientes']);
  }
}
