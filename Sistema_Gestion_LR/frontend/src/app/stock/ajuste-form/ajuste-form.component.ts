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
    fecha: ''
  };
  productoId: number|null = null;
  mensaje: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private stockService: StockService
  ) {}

  ngOnInit(): void {
    this.productoId = Number(this.route.snapshot.paramMap.get('id'));
    // Fecha por defecto: hoy
    this.ajuste.fecha = new Date().toISOString().substring(0, 10);
  }

  guardar() {
    if (!this.productoId) return;
    const ajusteData = {
      producto_id: this.productoId,
      tipo: 'AJUSTE',
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
}
