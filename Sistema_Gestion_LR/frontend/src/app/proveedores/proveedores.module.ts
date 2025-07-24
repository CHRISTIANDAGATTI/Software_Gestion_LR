import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProveedoresRoutingModule } from './proveedores-routing.module';
import { ProveedorListComponent } from './proveedor-list.component';
import { ProveedorFormComponent } from './proveedor-form.component';

@NgModule({
  declarations: [
    ProveedorListComponent,
    ProveedorFormComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ProveedoresRoutingModule
  ]
})
export class ProveedoresModule { }
