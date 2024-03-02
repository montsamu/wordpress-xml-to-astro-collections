This is a set of a few simple Python scripts to help
migrate from Wordpress (via an XML export) to a set of
AstroJS collections.

Currently, it's really only meant to support the following:

* Wordpress slugs like /year/month/day/title-of-post retained
* Astro posts collections in similarly nested folders

This might not be what you want, but even so, this might be a
decent starting point.

SETUP INSTRUCTIONS

1. pip install PyYAML
2. that's it

INSTRUCTIONS

```
python XML2Tags.py /path/to/your-wordpress-export.xml /path/to/your/astro/src/content/tags
python XML2Categories.py /path/to/your-wordpress-export.xml /path/to/your/astro/src/content/categories
python XML2Authors.py /path/to/your-wordpress-export.xml /path/to/your/astro/src/content/authors
python XML2Posts.py /path/to/your-wordpress-export.xml /path/to/your/astro/src/content/posts
python XML2Pages.py /path/to/your-wordpress-export.xml /path/to/your/astro/src/content/posts
```

NOTES:

* If there is a "blogger_author" post metadata, uses that as the author; ensure you actually have
  such an author in the system!

TODO

1. Add some tests
2. Also include some sample pages/layouts for folks to use?
3. Keep going and show folks how to add/edit posts?

EXAMPLE ASTRO SCHEMA

```
import { defineCollection, reference, z } from 'astro:content';

const postsCollection = defineCollection({
        type: 'content',
        schema: z.object({
                        title: z.string(),
                        author: reference('authors'),
                        pubDate: z.date(),
                        categories: z.array(reference('categories')),
                        tags: z.array(reference('tags')),
                        isPublished: z.boolean(),
                }),
});

const pagesCollection = defineCollection({
        type: 'content',
        schema: z.object({
                title: z.string(),
                isPublished: z.boolean(),
                sortOrder: z.number(),
                pubDate: z.date(),
                author: reference('authors'),
        }),
});

const categoryCollection = defineCollection({
  type: 'data',
  schema: z.object({
    name: z.string(),
    parent: reference('categories').nullable(),
  })
});

const tagCollection = defineCollection({
  type: 'data',
  schema: z.object({
    name: z.string(),
  })
});

const authorCollection = defineCollection({
  type: 'data',
  schema: z.object({
    email: z.string().email(),
    display_name: z.string(),
    last_name: z.string().nullable(),
    first_name: z.string().nullable(),
  })
});

export const collections = {
        posts: postsCollection,
        authors: authorCollection,
        categories: categoryCollection,
        tags: tagCollection,
        pages: pagesCollection,
};
```

