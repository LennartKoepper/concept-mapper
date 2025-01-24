import { Routes } from '@angular/router';
import { TextUploaderComponent } from './text-uploader/text-uploader.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { FileUploadComponent } from './file-upload/file-upload.component';
import { UrlProviderComponent } from './url-provider/url-provider.component';

export const routes: Routes = [
    {
        path: 'text',
        component: TextUploaderComponent,
    },
    {
        path: 'file-upload',
        component: FileUploadComponent
    },
    {
        path: 'url',
        component: UrlProviderComponent
    },
    { 
        path: '',   
        redirectTo: '/text',
        pathMatch: 'full' 
    },
    { 
        path: '**', 
        component: PageNotFoundComponent 
    },
];
