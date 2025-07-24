import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ClienteListComponent } from './cliente-list/cliente-list.component';
import { ClienteFormComponent } from './cliente-form/cliente-form.component';
import { ClientesRoutingModule } from './clientes-routing.module';

@NgModule({
  declarations: [ClienteListComponent, ClienteFormComponent],
  imports: [CommonModule, FormsModule, RouterModule, ClientesRoutingModule],
  exports: [ClienteListComponent, ClienteFormComponent]
})
export class ClientesModule { }
