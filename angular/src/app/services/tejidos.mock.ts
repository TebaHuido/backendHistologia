export interface ITejido {
    id: number;
    nombre: string;
    category: string;
    descripcion?: string;
    imagenUrl: string;
    alt: string;
}
export interface Categorias{
    id: number;
    name: string;
}
export interface Muestra {
    id: number;
    name: string;
    capturas: {
        id: number;
        name: string;
        image: string;
    }[];
    notas: {
        id: number;
        titulo: string;
        cuerpo: string;
        muestra: number[];
    }[];
    sistemas: string[];
}
export interface Tejido {
    capturas: { id: number; name: string; image: string; }[];
    notas: { id: number; titulo: string; cuerpo: string; muestra: number[]; }[];
    sistemas: string[];
    id: number;
    name: string;
    Categoria: number[];
    curso: any[];  // Si tienes una estructura específica para curso, puedes definirla en lugar de usar `any[]`
    organo: number[];
    sistema: string;
    imagenUrl: string;
}
export const tejidosArray: ITejido[] = [
    {
        id: 1,
        nombre: 'Tejido 1',
        category: 'pectoral',
        descripcion: 'Descripción del Tejido 1', // New property
        imagenUrl: 'https://concepto.de/wp-content/uploads/2019/04/histolog%C3%ADa-tejido-humano-e1554756738822.jpg',
        alt: 'Tejido 1'
    },
    {
        id: 2,
        nombre: 'Tejido 2',
        category: 'pectoral',
        descripcion: 'Descripción del Tejido 2', // New property
        imagenUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4A-NNkm3XUyTtIe3IVMfdwDoRdBQwABmSFw&s',
        alt: 'Tejido 2'
    },
    {
        id: 3,
        nombre: 'Tejido 3',
        category: 'facial',
        descripcion: 'Descripción del Tejido 3', // New property
        imagenUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTt0U78bpB4eGgzhoQpmhniTlGPykhu_Tueiw&s',
        alt: 'Tejido 3'
    },
    {
        id: 4,
        nombre: 'Tejido 4',
        category: 'facial',
        descripcion: 'Descripción del Tejido 4', // New property
        imagenUrl: 'https://www.pathologylive.com/practicas-histologia/images/11.jpg',
        alt: 'Tejido 4'
    },
]