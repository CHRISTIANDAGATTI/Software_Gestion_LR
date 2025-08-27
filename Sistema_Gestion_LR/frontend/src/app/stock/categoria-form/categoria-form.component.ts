import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StockService } from '../stock.service';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-categoria-form',
  templateUrl: './categoria-form.component.html'
})
export class CategoriaFormComponent implements OnInit {
  categoria: any = {
    nombre: ''
  };

  constructor(
    public route: ActivatedRoute,
    private router: Router,
    private stockService: StockService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.stockService.getCategoria().subscribe(data => {
        const cat = data.find((c: any) => c.id === id);
        if (cat) {
          this.categoria = { ...cat };
        }
      });
    } else {
      this.categoria = { nombre: '', descripcion: '' };
    }
  }

  guardarCambios() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.stockService.updateCategoria(id, this.categoria).subscribe({
        next: () => {
          alert('Categoría actualizada correctamente');
          this.router.navigate(['/stock']);
        },
        error: (error) => {
          console.error('Error al actualizar categoría:', error);
          alert('Error al actualizar categoría: ' + (error.error?.detail || error.message));
        }
      });
    } else {
      this.authService.getCurrentTenantId().then(tenant_id => {
        this.categoria.tenant_id = tenant_id;
        console.log('tenant_id enviado:', tenant_id);
        console.log('categoria enviada:', this.categoria);
        this.stockService.createCategoria(this.categoria).subscribe({
          next: () => {
            alert('Categoría creada correctamente');
            this.router.navigate(['/stock']);
          },
          error: (error) => {
            console.error('Error al crear categoría:', error);
            alert('Error al crear categoría: ' + (error.error?.detail || error.message));
          }
        });
      }).catch(error => {
        console.error('Error al obtener tenant_id:', error);
        alert('Error al obtener información del usuario');
      });
    }
  }

  volver() {
    this.router.navigate(['/stock']);
  }
}
