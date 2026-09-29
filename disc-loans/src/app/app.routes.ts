import { Routes } from '@angular/router';
import { DiscList } from './features/discs/disc-list/disc-list';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'discs-list' },
  { path: 'discs-list', component: DiscList },
  { path: 'discs', component: DiscList }
];
