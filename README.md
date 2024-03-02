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
python scripts/XML2Tags.py /path/to/your-wordpress-export.xml /path/to/your/astro/src/content/tags
python scripts/XML2Categories.py /path/to/your-wordpress-export.xml /path/to/your/astro/src/content/categories
python scripts/XML2Authors.py /path/to/your-wordpress-export.xml /path/to/your/astro/src/content/authors
python scripts/XML2Posts.py /path/to/your-wordpress-export.xml /path/to/your/astro/src/content/posts
python scripts/XML2Pages.py /path/to/your-wordpress-export.xml /path/to/your/astro/src/content/pages
```

NOTES:

* If there is a "blogger_author" post metadata, uses that as the author; ensure you actually have
  such an author in the system! (This is because I have a Wordpress site that migrated from a Blogger site...)
* Certain HTML content does not render well when included as markdown content; especially look out for
  deep indents (markdown thinks this is `code`)
* I didn't elect to retain the pages "parent" as a field in the schema, as the filesystem hierarchy suffices
* The data schemas do not explicitly include an 'id' field as this is implicitly created by AstroJS
  from the filename

TODO

1. Add some tests
2. Also include some sample pages/layouts for folks to use directly, instead of just in the README?
3. Include an RSS example?
4. Keep going and show folks how to add/edit posts?

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

EXAMPLE ASTRO PAGES:

```
# /index.astro

---
import { getCollection } from 'astro:content';

// TODO: use pagination?
const allPosts = await getCollection("posts", ({ data }) => {
      return data.isPublished == true;
});

// TODO: use locale?
const posts = allPosts.sort((a,b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---
... {posts.map()} ...
```

```
# /[...slug].astro -- handles "pages" content

---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
    const pages = await getCollection("pages", ({ data }) => {
      return data.isPublished == true;
    });
    return pages.map(
      ({
        data: { title, pubDate, author },
        render,
        slug,
      }) => {
        return {
            params: { slug },
            props: {
              render,
              title,
              pubDate,
              author,
            },
        };
    });
}

const { slug } = Astro.params;

const { render, title, pubDate, author } = Astro.props;

const { Content } = await render();
---
... {title} {author.id} <Content/> ...
```

```
# /author/[id].astro

---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
    const authors = await getCollection("authors");
    return authors.map(author => ({
        params: { id: author.id }, props: { author },
    }));
}

const { author } = Astro.props;

const filteredPosts = await getCollection("posts", ({ data }) => {
  return data.author.id == author.id
});

const posts = filteredPosts.sort((a,b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---
... {author.name} ...
```

```
# /category/[id].astro

---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
    const categories = await getCollection("categories");
    return categories.map(category => ({
        params: { id: category.id }, props: { category },
    }));
}

const { category } = Astro.props;

const filteredPosts = await getCollection("posts", ({ data }) => {
  return data.categories.find((element) => element.id == category.id);
});

const posts = filteredPosts.sort((a,b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---
... {category.name} ...
```

```
# /tag/[id].astro

---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
    const tags = await getCollection("tags");
    return tags.map(tag => ({
        params: { id: tag.id }, props: { tag },
    }));
}

const { tag } = Astro.props;

const filteredPosts = await getCollection("posts", ({ data }) => {
  return data.tags.find((element) => element.id == tag.id);
});

const posts = filteredPosts.sort((a,b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---
... {tag.name} ...
```

```
# /[year]/index.astro -- handles yearly archives

---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
    const posts = await getCollection("posts", ({ data }) => {
      return data.isPublished == true;
    });
    return Array.from(new Set(posts.map(
      ({
        slug,
      }) => {
        return {
            params: { year: slug.substring(0,4) },
            props: {},
        };
    })).values());
}

const { year } = Astro.params;

const slug = `${year}`

const filteredPosts = await getCollection("posts", (post) => {
  return post.slug.startsWith(slug);
});

const posts = filteredPosts.sort((a,b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---
...
```

```
# /[year]/[month]/index.astro -- handles monthly archives

---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
    const posts = await getCollection("posts", ({ data }) => {
      return data.isPublished == true;
    });
    return Array.from(new Set(posts.map(
      ({
        slug,
      }) => {
        return {
            params: { year: slug.substring(0,4), month: slug.substring(5,7) },
            props: {},
        };
    })).values());
}

const { year, month } = Astro.params;

const slug = `${year}/${month}`

const filteredPosts = await getCollection("posts", (post) => {
  return post.slug.startsWith(slug);
});

const posts = filteredPosts.sort((a,b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---
...
```

```
# /[year]/[month]/[day]/index.astro -- handles daily archives

---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
    const posts = await getCollection("posts", ({ data }) => {
      return data.isPublished == true;
    });
    return Array.from(new Set(posts.map(
      ({
        slug,
      }) => {
        return {
            params: { year: slug.substring(0,4), month: slug.substring(5,7), day: slug.substring(8,10) },
            props: {},
        };
    })).values());
}

const { year, month, day } = Astro.params;

const slug = `${year}/${month}/${day}`

const filteredPosts = await getCollection("posts", (post) => {
  return post.slug.startsWith(slug);
});

const posts = filteredPosts.sort((a,b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---
...
```

```
# /[year]/[month]/[day]/[...slug].astro -- handles posts

---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
    const posts = await getCollection("posts", ({ data }) => {
      return data.isPublished == true;
    });
    return posts.map(
      ({
        data: { title, pubDate, author, categories, tags },
        render,
        slug,
      }) => {
        return {
            params: { year: slug.substring(0,4), month: slug.substring(5,7), day: slug.substring(8,10), slug: slug.substring(11) },
            props: {
              render,
              title,
              pubDate,
              author,
              categories,
              tags,
            },
        };
    });
}

const { slug } = Astro.params;

const { render, title, pubDate, author, categories, tags } = Astro.props;

const { Content } = await render();
---
... {title} by {author.id} {categories.map()} {tags.map()} <Content/> ...
```
