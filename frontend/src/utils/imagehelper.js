function detectMimeFromBase64(base64) {
    if (!base64) {
        return 'image/jpeg';
    }

    if (base64.startsWith('iVBOR')) {
        return 'image/png';
    }

    if (base64.startsWith('/9j/')) {
        return 'image/jpeg';
    }

    if (base64.startsWith('UklGR')) {
        return 'image/webp';
    }

    return 'image/jpeg';
}

export function getImageSrc(baseImage) {
    if (!baseImage) {
        return '';
    }

    if (baseImage.startsWith('data:image')) {
        return baseImage;
    }

    if (baseImage.startsWith('http://') || baseImage.startsWith('https://')) {
        return baseImage;
    }

    const mime = detectMimeFromBase64(baseImage);
    return `data:${mime};base64,${baseImage}`;
}

export default getImageSrc;