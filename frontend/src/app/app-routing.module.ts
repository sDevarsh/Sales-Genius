
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';

import { ServicesDetailsComponent } from './services-details/services-details.component';
import { ExamplesComponent } from './examples/examples.component';
import { HowToUseComponent } from './how-to-use/how-to-use.component';

export const routes: Routes = [
  { path: '#', pathMatch: 'full', redirectTo: 'home' },
  { path: 'home', component: HomeComponent },
  { path: 'services-details', component: ServicesDetailsComponent },
  { path: 'examples', component: ExamplesComponent },
  { path: 'how-to-use', component: HowToUseComponent },
  { path: '**', pathMatch: 'full', redirectTo: 'home' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
