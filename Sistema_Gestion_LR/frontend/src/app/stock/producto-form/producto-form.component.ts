import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StockService } from '../stock.service';

@Component({
  selector: 'app-producto-form',
  templateUrl: './producto-form.component.html'
})
export class ProductoFormComponent implements OnInit {
  producto: any = { nombre: '', descripcion: '', precio: 0 };
  isEdit: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private stockService: StockService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEdit = true;
      this.stockService.getProducto().subscribe(data => {
        this.producto = data;
      });
    }
  }

  guardar() {
    if (this.isEdit) {
      this.stockService.updateProducto(this.producto.id, this.producto).subscribe(() => {
        this.router.navigate(['/stock']);
      });
    }
  }
}
