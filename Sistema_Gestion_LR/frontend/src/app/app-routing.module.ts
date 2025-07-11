import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './auth/login/login.component';
import { RegistroComponent } from './auth/registro/registro.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ClienteListComponent } from './clientes/cliente-list.component';
import { ProveedorListComponent } from './proveedores/proveedor-list.component';
import { VentaListComponent } from './ventas/venta-list.component';
import { CompraListComponent } from './compras/compra-list.component';
import { PresupuestoListComponent } from './presupuesto/presupuesto-list.component';



const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'registro', component: RegistroComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'stock', loadChildren: () => import('./stock/stock.module').then(m => m.StockModule) },
  { path: 'clientes', component: ClienteListComponent },
  { path: 'proveedores', component: ProveedorListComponent },
  { path: 'ventas', component: VentaListComponent },
  { path: 'compras', component: CompraListComponent },
  { path: 'presupuesto', component: PresupuestoListComponent },
  { path: '**', redirectTo: 'home' },
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
