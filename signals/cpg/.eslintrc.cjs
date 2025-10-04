 module.exports = {
    root:true,
    env: {browser:true, es2020:true }, 
    extends: [
        'airbnb', 
        'airbnb-typescript', 
        'airbnb-hooks', 
        'plugin:@typescript-eslint/recommended', 
        'plugin:react-hooks/recommended',
        'plugin:pretiier/recommended'
    ], 
    ignorePatterns:['dist', '.eslintrc.cjs', 'vite.config.ts'],
    parser: '@typescript-eslint/parser', 
    parserOptions:{
        project : './tsconfig.json'
    }, 
    plugins: ['react', '@typescript-eslint', 'prettier', 'react-refresh'], 
    rules: {
        'react-refresh/only-expert-components':[
            'warn',
            {
                allowConstantExport: true 
            }, 
        ],
        'react/react-in-jsx-scope':0, 
        'react/no-unstable-nested-components':0,
        'import/prefer-default-export':0,
        'import/extensions':0,
        'react/require-default-props':0,
        '@typescript-eslint/no-explicit-any':0 

    },
 }