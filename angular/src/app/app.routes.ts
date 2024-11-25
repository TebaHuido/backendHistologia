import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { SettingsComponent } from './settings/settings.component';
import { NotesComponent } from './notes/notes.component';
import { TejidoComponent } from './tejido/tejido.component';
import { UplimageComponent } from './uplimage/uplimage.component';
import { LoginComponent } from './login/login.component';
import { TissueviewerComponent } from './tissueviewer/tissueviewer.component';
import { ImageProcessorComponent } from './image-processor/image-processor.component';
import { TestingviewComponent } from './testingview/testingview.component';
import { FilterComponent } from './filter/filter.component';
export const routes: Routes = [
    { path: '', component: HomeComponent, title: 'Muestras Histológicas UTA' },
    { path: 'settings', component: SettingsComponent },
    { path: 'notes', component: NotesComponent },
    { path: 'uploadimg', component: UplimageComponent },
    { path: 'tejido', component: TejidoComponent },
    { path: 'tejido/:id', component: TejidoComponent },
    { path: 'sesion', component: LoginComponent },
    { path: 'tissueviewer', component: TissueviewerComponent },
    { path: 'playground', component: ImageProcessorComponent},
    { path : 'test', component: FilterComponent}
];
