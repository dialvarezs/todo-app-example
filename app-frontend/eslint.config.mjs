import antfu from '@antfu/eslint-config'

export default antfu(
  {
    rules: {
      'style/brace-style': 'off',
      'antfu/consistent-list-newline': 'off',
      'perfectionist/sort-imports': [
        'error',
        {
          internalPattern: ['^@/.*'],
          groups: [
            'vue',
            ['builtin', 'external'],
            'internal',
            ['parent-type', 'sibling-type', 'index-type'],
            ['parent', 'sibling', 'index'],
            'object',
            'unknown',
            'components',
            'type',
            'internal-type',
          ],
          customGroups: {
            value: {
              vue: ['^vue.*'],
              components: ['^@/components/.*'],
            },
          },
        },
      ],
    },
  },
)
