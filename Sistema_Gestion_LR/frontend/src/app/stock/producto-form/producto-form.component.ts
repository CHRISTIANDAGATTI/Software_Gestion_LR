import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StockService } from '../stock.service';

@Component({
  selector: 'app-producto-form',
  templateUrl: './producto-form.component.html'
})
export class ProductoFormComponent implements OnInit {
  producto: any = { nombre: '', descripcion: '', precio: 0, categoria_id: null, codigo: '' };
  categorias: any[] = [];
  productos: any[] = [];
  isEdit: boolean = false;
  codigoError: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private stockService: StockService
  ) {}

  ngOnInit(): void {
    // Cargar categorías y productos
    this.stockService.getCategoria().subscribe(cats => {
      this.categorias = cats;
      this.stockService.getProducto().subscribe(prods => {
        this.productos = prods;
        // Si es edición, cargar producto
        const id = this.route.snapshot.paramMap.get('id');
        if (id) {
          this.isEdit = true;
          this.stockService.getProducto(Number(id)).subscribe(data => {
            this.producto = data;
            if (this.producto.categoria && typeof this.producto.categoria === 'object') {
              this.producto.categoria_id = this.producto.categoria.id;
            }
          });
        } else {
          this.isEdit = false;
          this.producto = { nombre: '', descripcion: '', precio: 0, cantidad: 0, categoria_id: null, codigo: '' };
        }
      });
    });
  }

  guardar() {
    // Validar código único
    const codigoExiste = this.productos.some(p => p.codigo === this.producto.codigo && (!this.isEdit || p.id !== this.producto.id));
    if (codigoExiste) {
      this.codigoError = 'El código ya existe para otro producto.';
      return;
    }
    this.codigoError = '';
    if (this.isEdit) {
      this.stockService.updateProducto(this.producto.id, this.producto).subscribe(() => {
        this.router.navigate(['/stock']);
      });
    } else {
      this.stockService.createProducto(this.producto).subscribe(() => {
        this.router.navigate(['/stock']);
      });
    }
  }
}
