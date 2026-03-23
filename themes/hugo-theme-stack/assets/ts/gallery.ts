declare global {
    interface Window {
        PhotoSwipe: any;
        PhotoSwipeUI_Default: any
    }
}

interface PhotoSwipeItem {
    w: number;
    h: number;
    src: string;
    msrc: string;
    title?: string;
    el: HTMLElement;
}

class StackGallery {
    private galleryUID: number;
    private items: PhotoSwipeItem[] = [];

    constructor(container: HTMLElement, galleryUID = 1) {
        if (window.PhotoSwipe == undefined || window.PhotoSwipeUI_Default == undefined) {
            console.error("PhotoSwipe lib not loaded.");
            return;
        }

        this.galleryUID = galleryUID;

        StackGallery.createGallery(container);
        this.loadItems(container);
        this.bindClick();
    }

    private loadItems(container: HTMLElement) {
        this.items = [];

        const figures = container.querySelectorAll('figure.gallery-image');

        for (const el of figures) {
            const figcaption = el.querySelector('figcaption'),
                img = el.querySelector('img') as HTMLImageElement;

            const width = StackGallery.getImageDimension(img, 'width');
            const height = StackGallery.getImageDimension(img, 'height');

            let aux: PhotoSwipeItem = {
                w: width,
                h: height,
                src: img.src,
                msrc: img.getAttribute('data-thumb') || img.src,
                el: el
            }

            if (figcaption) {
                aux.title = figcaption.innerHTML;
            }

            this.items.push(aux);
        }
    }

    private static getImageDimension(img: HTMLImageElement, dimension: 'width' | 'height'): number {
        const attrValue = img.getAttribute(dimension)?.trim();
        if (attrValue && /^\d+$/.test(attrValue)) {
            return parseInt(attrValue, 10);
        }

        if (dimension === 'width') {
            return img.naturalWidth || img.width;
        }

        return img.naturalHeight || img.height;
    }

    public static createGallery(container: HTMLElement) {
        /// The process of wrapping image with figure tag is done using JavaScript instead of only Hugo markdown render hook
        /// because it can not detect whether image is being wrapped by a link or not
        /// and it lead to a invalid HTML construction (<a><figure><img></figure></a>)

        const images = container.querySelectorAll('img');
        for (const img of Array.from(images) as HTMLImageElement[]) {
            if (img.closest('figure.gallery-image')) continue;

            const standaloneWrapper = StackGallery.getStandaloneWrapper(container, img);
            if (!standaloneWrapper) continue;

            const link = img.parentElement?.tagName == 'A' ? img.parentElement as HTMLAnchorElement : null;
            let el: HTMLElement = link || img;

            /// Wrap image with figure tag, with flex-grow and flex-basis values extracted from img's data attributes
            const figure = document.createElement('figure');
            figure.className = 'gallery-image';
            figure.style.setProperty('flex-grow', img.getAttribute('data-flex-grow') || '1');
            figure.style.setProperty('flex-basis', img.getAttribute('data-flex-basis') || '0');
            el.parentElement.insertBefore(figure, el);
            figure.appendChild(el);

            /// Add figcaption if it exists
            const alt = img.getAttribute('alt')?.trim();
            if (alt) {
                const figcaption = document.createElement('figcaption');
                figcaption.innerText = alt;
                figure.appendChild(figcaption);
            }

            /// Wrap img tag with <a> tag if image was not wrapped by <a> tag
            if (!link) {
                const a = document.createElement('a');
                a.href = img.src;
                a.setAttribute('target', '_blank');
                a.setAttribute('rel', 'noreferrer');
                img.parentNode.insertBefore(a, img);
                a.appendChild(img);
            }
        }

        const figuresEl = container.querySelectorAll('figure.gallery-image');

        let currentGallery = [];

        for (const figure of figuresEl) {
            if (!currentGallery.length) {
                /// First iteration
                currentGallery = [figure];
            }
            else if (figure.previousElementSibling === currentGallery[currentGallery.length - 1]) {
                /// Adjacent figures
                currentGallery.push(figure);
            }
            else if (currentGallery.length) {
                /// End gallery
                StackGallery.wrap(currentGallery);
                currentGallery = [figure];
            }
        }

        if (currentGallery.length > 0) {
            StackGallery.wrap(currentGallery);
        }
    }

    private static getStandaloneWrapper(container: HTMLElement, img: HTMLImageElement): HTMLElement | null {
        const wrapper = img.closest('p, div');
        if (!wrapper || !container.contains(wrapper)) return null;
        if (wrapper.matches('.gallery, figure, .highlight, .notice')) return null;
        if (!this.isStandaloneImageWrapper(wrapper, img)) return null;

        if (wrapper.textContent.trim() == '') {
            wrapper.classList.add('no-text');
        }

        return wrapper.classList.contains('no-text') ? wrapper as HTMLElement : null;
    }

    private static isStandaloneImageWrapper(wrapper: Element, img: HTMLImageElement): boolean {
        const directImages = Array.from(wrapper.querySelectorAll('img'))
            .filter(child => child.closest('p, div') === wrapper);
        if (!directImages.includes(img)) return false;

        const hasNestedBlocks = Array.from(wrapper.children).some(child => {
            if (child === img || child.contains(img)) return false;
            return child.tagName !== 'A' && child.tagName !== 'BR';
        });

        return !hasNestedBlocks;
    }

    /**
     * Wrap adjacent figure tags with div.gallery
     * @param figures 
     */
    public static wrap(figures: HTMLElement[]) {
        const galleryContainer = document.createElement('div');
        galleryContainer.className = 'gallery';

        const parentNode = figures[0].parentNode,
            first = figures[0];

        parentNode.insertBefore(galleryContainer, first)

        for (const figure of figures) {
            galleryContainer.appendChild(figure);
        }
    }

    public open(index: number) {
        const pswp = document.querySelector('.pswp') as HTMLDivElement;
        const ps = new window.PhotoSwipe(pswp, window.PhotoSwipeUI_Default, this.items, {
            index: index,
            galleryUID: this.galleryUID,
            getThumbBoundsFn: (index) => {
                const thumbnail = this.items[index].el.getElementsByTagName('img')[0],
                    pageYScroll = window.pageYOffset || document.documentElement.scrollTop,
                    rect = thumbnail.getBoundingClientRect();

                return { x: rect.left, y: rect.top + pageYScroll, w: rect.width };
            }
        });

        ps.init();
    }

    private bindClick() {
        for (const [index, item] of this.items.entries()) {
            const a = item.el.querySelector('a');
            if (!a) continue;

            a.addEventListener('click', (e) => {
                e.preventDefault();
                this.open(index);
            })
        }
    }
}

export default StackGallery;
