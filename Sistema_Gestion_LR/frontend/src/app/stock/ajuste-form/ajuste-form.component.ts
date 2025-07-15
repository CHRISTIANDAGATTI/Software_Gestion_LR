import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StockService } from '../stock.service';

@Component({
  selector: 'app-ajuste-form',
  templateUrl: './ajuste-form.component.html',
  styleUrls: ['./ajuste-form.component.css']
})
export class AjusteFormComponent implements OnInit {
  ajuste: any = {
    cantidad: null,
    observaciones: '',
    fecha: '',
    motivo: null
  };
  productoId: number|null = null;
  mensaje: string = '';
  motivos: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private stockService: StockService
  ) {}

  ngOnInit(): void {
    this.productoId = Number(this.route.snapshot.paramMap.get('id'));
    // Fecha por defecto: hoy
    this.ajuste.fecha = new Date().toISOString().substring(0, 10);
    // Obtener motivos desde el backend
    this.stockService.getMotivosOperacion().subscribe({
      next: (data) => {
        // Excluir Compra y Venta del select de ajuste
        this.motivos = data.filter((motivo: any) =>
          motivo.nombre !== 'Compra' && motivo.nombre !== 'Venta'
        );
      },
      error: () => {
        this.motivos = [];
      }
    });
  }

  guardar() {
    if (!this.productoId || !this.ajuste.motivo) return;
    const ajusteData = {
      producto_id: this.productoId,
      tipo_operacion_id: this.ajuste.motivo,
      cantidad: this.ajuste.cantidad,
      observaciones: this.ajuste.observaciones,
      fecha: this.ajuste.fecha
    };
    this.stockService.registrarAjuste(ajusteData).subscribe({
      next: () => {
        this.mensaje = 'Ajuste registrado correctamente.';
        setTimeout(() => this.router.navigate(['/stock']), 1200);
      },
      error: () => {
        this.mensaje = 'Error al registrar el ajuste.';
      }
    });
  }

  volver() {
    this.router.navigate(['/stock']);
  }
}
