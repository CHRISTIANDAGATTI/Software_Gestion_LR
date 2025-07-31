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
    // Validaciones previas
    if (!this.proveedor.nombre && !this.proveedor.razon_social) {
      alert('Debe completar al menos Nombre o Razón social.');
      return;
    }
    if (this.proveedor.condicion_fiscal && this.proveedor.condicion_fiscal !== 'Consumidor Final' && !this.proveedor.cuit) {
      alert('Si la condición fiscal no es Consumidor Final, debe ingresar el CUIT.');
      return;
    }
    if (!this.proveedor.cuit && !this.proveedor.dni) {
      alert('Debe completar al menos CUIT o DNI.');
      return;
    }
    if (this.proveedor.dni && !/^\d{7,}$/.test(this.proveedor.dni)) {
      alert('El DNI debe ser numérico y tener al menos 7 dígitos.');
      return;
    }
    if (this.proveedor.cuit && !/^\d{11}$/.test(this.proveedor.cuit)) {
      alert('El CUIT debe ser numérico y tener 11 dígitos.');
      return;
    }
    if (this.proveedor.telefono && !/^\d{6,}$/.test(this.proveedor.telefono)) {
      alert('El teléfono debe ser numérico y tener al menos 6 dígitos.');
      return;
    }
    if (this.proveedor.email && !/^\S+@\S+\.\S+$/.test(this.proveedor.email)) {
      alert('El formato del email es inválido.');
      return;
    }
    if (this.editando) {
      // Aquí iría la lógica de edición
    } else {
      // Obtener tenant_id antes de crear
      import('../auth/auth.service').then(async ({ AuthService }) => {
        const authService = new AuthService();
        const tenant_id = await authService.getCurrentTenantId();
        this.proveedor.tenant_id = tenant_id;
        this.proveedorService.createProveedor(this.proveedor).subscribe({
          next: () => this.router.navigate(['/proveedores']),
          error: err => {
            if (err?.error?.detail?.toLowerCase().includes('duplicate') || err?.error?.detail?.toLowerCase().includes('ya existe')) {
              alert('El email o CUIT ya está registrado.');
            } else {
              alert('Error al crear proveedor: ' + (err?.error?.detail || err.message));
            }
          }
        });
      });
    }
  }

  cancelar() {
    this.router.navigate(['/proveedores']);
  }
}
