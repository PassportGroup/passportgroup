let mix = require('laravel-mix');
const tailwindcss = require("tailwindcss");
const path = require('path')

mix.js('apps/frontend/js/index.js', 'build')
    .extract()
    .sass('apps/frontend/css/app.scss', 'build')
    .vue({ runtimeOnly: true })
    .setPublicPath('static')
    .options({
        processCssUrls: false,
        postCss: [
            tailwindcss('tailwind.config.js'),
        ],
    })
    .autoload({
        "cash-dom": ["cash"]
    })
    .webpackConfig({
        output: {
            publicPath: '/static/',
            chunkFilename: 'build/[name].js?id=[chunkhash]',
        },
        resolve: {
            extensions: ['.js', '.vue', '.json'],
            alias: {
                'vue$': 'vue/dist/vue.runtime.esm.js',
                '@': path.resolve('apps/frontend/js'),
            }
        },
    })
    .version()