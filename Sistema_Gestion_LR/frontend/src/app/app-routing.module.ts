import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './auth/login/login.component';
import { RegistroComponent } from './auth/registro/registro.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProveedorListComponent } from './proveedores/proveedor-list.component';
import { VentaListComponent } from './ventas/venta-list.component';
import { CompraListComponent } from './compras/compra-list.component';
import { PresupuestoListComponent } from './presupuesto/presupuesto-list.component';
import { AuthGuard } from './auth/auth.guard';
import { AdminGuard } from './admin/admin.guard';
import { AdminPanelComponent } from './admin/admin-panel.component';



const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'registro', component: RegistroComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'stock', loadChildren: () => import('./stock/stock.module').then(m => m.StockModule), canActivate: [AuthGuard] },
  { path: 'clientes', loadChildren: () => import('./clientes/clientes.module').then(m => m.ClientesModule), canActivate: [AuthGuard] },
  { path: 'proveedores', loadChildren: () => import('./proveedores/proveedores.module').then(m => m.ProveedoresModule), canActivate: [AuthGuard] },
  { path: 'ventas', component: VentaListComponent, canActivate: [AuthGuard] },
  { path: 'compras', component: CompraListComponent, canActivate: [AuthGuard] },
  { path: 'presupuesto', component: PresupuestoListComponent, canActivate: [AuthGuard] },
  {
    path: 'admin',
    component: AdminPanelComponent,
    canActivate: [AdminGuard]
  },
  { path: '**', redirectTo: 'home' },
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
