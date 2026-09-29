import { Routes } from '@angular/router';
import { DiscList } from './features/discs/disc-list/disc-list';
import { LoanForm } from './features/loans/loan-form/loan-form';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'discs-list' },
  { path: 'discs-list', component: DiscList },
  { path: 'discs', component: DiscList },
  { path: 'loans/:discId', component: LoanForm },
];
