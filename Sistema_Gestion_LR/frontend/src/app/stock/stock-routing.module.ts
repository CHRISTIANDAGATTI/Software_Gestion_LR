import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StockListComponent } from './stock-list/stock-list.component';
import { ProductoFormComponent } from './producto-form/producto-form.component';
import { CategoriaFormComponent } from './categoria-form/categoria-form.component';
import { AjusteFormComponent } from './ajuste-form/ajuste-form.component';
import { CategoriaReasignarComponent } from './categoria-reasignar/categoria-reasignar.component';


const routes: Routes = [
  { path: '', component: StockListComponent },
  { path: 'producto/editar/:id', component: ProductoFormComponent },
  { path: 'producto/agregar', component: ProductoFormComponent },
  { path: 'categoria/editar/:id', component: CategoriaFormComponent },
  { path: 'categoria/agregar', component: CategoriaFormComponent },
  { path: 'producto/ajustar/:id', component: AjusteFormComponent },
  { path: 'categoria/reasignar/:id', component: CategoriaReasignarComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StockRoutingModule { }

