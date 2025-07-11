import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { FooterComponent } from './shared/footer/footer.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './auth/login/login.component';
import { RegistroComponent } from './auth/registro/registro.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NavbarPublicoComponent } from './shared/navbar/navbar-publico.component';
import { NavbarPrivadoComponent } from './shared/navbar/navbar-privado.component';
import { ClienteListComponent } from './clientes/cliente-list.component';
import { ProveedorListComponent } from './proveedores/proveedor-list.component';
import { VentaListComponent } from './ventas/venta-list.component';
import { CompraListComponent } from './compras/compra-list.component';
import { PresupuestoListComponent } from './presupuesto/presupuesto-list.component';

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    HomeComponent,
    LoginComponent,
    RegistroComponent,
    DashboardComponent,
    NavbarPublicoComponent,
    NavbarPrivadoComponent,
    ClienteListComponent,
    ProveedorListComponent,
    VentaListComponent,
    CompraListComponent,
    PresupuestoListComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

