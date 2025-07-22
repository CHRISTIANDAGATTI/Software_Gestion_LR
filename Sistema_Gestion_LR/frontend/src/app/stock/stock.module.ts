import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';

import { StockRoutingModule } from './stock-routing.module';
import { StockListComponent } from './stock-list/stock-list.component';
import { ProductoFormComponent } from './producto-form/producto-form.component';
import { CategoriaFormComponent } from './categoria-form/categoria-form.component';
import { AjusteFormComponent } from './ajuste-form/ajuste-form.component';
import { CategoriaReasignarComponent } from './categoria-reasignar/categoria-reasignar.component';
import { CategoriaListComponent } from './categoria-list/categoria-list.component';
import { ConfirmDialogComponent } from './confirm-dialog.component';


@NgModule({
  declarations: [
    StockListComponent,
    ProductoFormComponent,
    CategoriaFormComponent,
    AjusteFormComponent,
    CategoriaReasignarComponent,
    CategoriaListComponent,
    ConfirmDialogComponent
  ],
  imports: [
    CommonModule,
    StockRoutingModule,
    FormsModule,
    MatDialogModule
  ]
})
export class StockModule { }
