import { Component, OnInit } from '@angular/core';
import { ProveedorService } from './proveedor.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-proveedor-form',
  templateUrl: './proveedor-form.component.html'
})
export class ProveedorFormComponent implements OnInit {
  proveedor: any = {
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
    private proveedorService: ProveedorService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.editando = true;
      this.proveedorService.getProveedor(+id).subscribe({
        next: data => this.proveedor = data,
        error: err => alert('Error al cargar proveedor: ' + (err?.error?.detail || err.message))
      });
    }
  }

  guardarProveedor() {
    if (this.editando) {
      // Aquí iría la lógica de edición
    } else {
      this.proveedorService.createProveedor(this.proveedor).subscribe({
        next: () => this.router.navigate(['/proveedores']),
        error: err => alert('Error al crear proveedor: ' + (err?.error?.detail || err.message))
      });
    }
  }

  cancelar() {
    this.router.navigate(['/proveedores']);
  }
}
